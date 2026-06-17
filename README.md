# eVTOL Rotor Sizing Computational API Backend

[![Live Frontend Demo](https://img.shields.io/badge/Live_Demo-Vercel-blue?style=for-the-badge&logo=vercel)](https://sizing-final.vercel.app/)
[![Backend Repository](https://img.shields.io/badge/Codebase-GitHub-green?style=for-the-badge&logo=github)](https://github.com/shashwatt22/evtol-sizing-backend)

A modular Django REST backend engineered to execute complex multi-configuration aerodynamic sizing workflows...

## 🛠️ API Routing Architecture
The central endpoint (`/api/size/`) acts as a dynamic orchestration layer, parsing request payloads and evaluating structural constraints natively:
* **Multirotor Routing:** Executes custom parameter scaling via `calculate_multirotor()`.
* **Lift + Cruise Routing:** Routes vector propulsion sizing tasks via `calculate_lift_plus_cruise()`.
* **Tiltrotor Routing:** Runs variable-axis angle estimations via `calculate_tiltrotor()`.
* **Single Main Rotor (SMR):** Evaluates traditional helicopter rotor profiles via `calculate_smr()`.

## 📈 System Robustness & Logging
* Enforces payload validation, utilizing structured exception blocks to trap mathematical runtime errors (`status=500`) and JSON parse mistakes (`status=400`).
* Features comprehensive server-side system tracing (`[DEBUG]`, `[INFO]`, `[ERROR]`) providing clear audit trails for engineering design tracking.
