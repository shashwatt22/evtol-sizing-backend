# eVTOL Rotor Sizing Computational API Backend

A modular Django REST backend engineered to execute complex multi-configuration aerodynamic sizing workflows for electric Vertical Takeoff and Landing (eVTOL) aircraft. This API decouples user inputs from the core propulsion physics models, processing structural calculations for 4 distinct aircraft configurations.

## 🛠️ API Routing Architecture
The central endpoint (`/api/size/`) acts as a dynamic orchestration layer, parsing request payloads and evaluating structural constraints natively:
* **Multirotor Routing:** Executes custom parameter scaling via `calculate_multirotor()`.
* **Lift + Cruise Routing:** Routes vector propulsion sizing tasks via `calculate_lift_plus_cruise()`.
* **Tiltrotor Routing:** Runs variable-axis angle estimations via `calculate_tiltrotor()`.
* **Single Main Rotor (SMR):** Evaluates traditional helicopter rotor profiles via `calculate_smr()`.

## 📈 System Robustness & Logging
* Enforces payload validation, utilizing structured exception blocks to trap mathematical runtime errors (`status=500`) and JSON parse mistakes (`status=400`).
* Features comprehensive server-side system tracing (`[DEBUG]`, `[INFO]`, `[ERROR]`) providing clear audit trails for engineering design tracking.
