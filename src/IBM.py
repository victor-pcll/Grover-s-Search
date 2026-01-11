from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

def run_on_ibm_hardware(qc, shots=4000):
    print("1. Connexion à IBM Quantum...")
    try:
        # On utilise le canal qui a marché dans vos logs
        # On ne précise pas l'instance, on laisse Qiskit choisir 'open-instance' tout seul
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return None

    print("2. Recherche du backend le moins occupé...")
    try:
        # On cherche une vraie machine (simulator=False)
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=qc.num_qubits)
        print(f"   ✅ Machine trouvée : {backend.name} ({backend.num_qubits} qubits)")
    except Exception as e:
        print(f"❌ Aucune machine disponible : {e}")
        return None

    print(f"3. Transpilation pour {backend.name} (Optimisation niveau 3)...")
    # L'optimisation niveau 3 est cruciale pour minimiser le bruit
    t_qc = transpile(qc, backend, optimization_level=3)
    
    print(f"4. Envoi du Job (Shots={shots})...")
    sampler = Sampler(mode=backend)
    job = sampler.run([t_qc], shots=shots)
    
    job_id = job.job_id()
    print(f"   🚀 Job envoyé ! ID : {job_id}")
    print("   ⚠️  IMPORTANT : Copiez cet ID. Si ça plante, vous pourrez récupérer les résultats plus tard.")
    print("   ⏳ En attente des résultats (cela peut prendre du temps selon la file d'attente)...")
    
    try:
        # On attend la fin du calcul
        result = job.result()
        
        # Extraction des résultats (Compatible Sampler V2)
        pub_result = result[0]
        # On cherche le registre de mesure (souvent 'meas' ou 'c')
        if hasattr(pub_result.data, 'meas'):
            counts = pub_result.data.meas.get_counts()
        elif hasattr(pub_result.data, 'c'):
             counts = pub_result.data.c.get_counts()
        else:
            first_key = list(pub_result.data.keys())[0]
            counts = getattr(pub_result.data, first_key).get_counts()
            
        print("✅ Résultats reçus !")
        return counts

    except Exception as e:
        print(f"❌ Erreur lors de l'attente/récupération : {e}")
        print(f"   Vous pourrez réessayer plus tard avec : service.job('{job_id}').result()")
        return None

def test_connection(api_token):
    print(f"Test de connexion avec le token : {api_token[:5]}...{api_token[-5:]}")
    
    # 1. Essai automatique
    try:
        print("\nTentative 1 : Auto-découverte...")
        service = QiskitRuntimeService(token=api_token)
        print(" -> Succès ! Canal détecté :", service.channel)
        print(" -> Instance sauvegardée :", service.active_account().get('instance'))
    except Exception as e:
        print(f" -> Echec Auto : {e}")
        
        # 2. Essai forcé 'ibm_quantum' (Compte Open Plan standard)
        try:
            print("\nTentative 2 : Forcer channel='ibm_quantum'...")
            service = QiskitRuntimeService(channel="ibm_quantum", token=api_token)
            print(" -> Succès !")
        except Exception as e2:
            print(f" -> Echec Total. Vérifiez votre Token sur le site IBM.")
            return

    # 3. Lister les machines disponibles
    print("\nRecherche de machines réelles accessibles...")
    try:
        # On liste toutes les machines réelles (pas les simulateurs)
        backends = service.backends(simulator=False, operational=True)
        if backends:
            print(f" -> {len(backends)} machines trouvées.")
            print(f" -> La moins occupée est : {service.least_busy(simulator=False).name}")
        else:
            print(" -> Aucune machine réelle trouvée (maintenance ou file pleine).")
            print(" -> Essayez avec simulator=True pour voir si la connexion marche au moins.")
            
    except Exception as e:
        print(f"Erreur lors de la recherche de backends : {e}")