# Take-Home Engineering Challenge: Device Monitor Dashboard

**Role:** Generalist Engineer (Fresh Graduate)  
**Duration:** Approx. 2 Days  
**Keyword:** Monitor

## >à Overview

Create a **Device Monitoring Dashboard** web application that displays system metrics for a list of devices (e.g., servers, laptops, IoT units). The goal is to simulate a live monitoring tool where each device reports key data points like CPU usage, temperature, and status.

## =Ì Objectives

1. **System Design**
   - Define system components (frontend, backend, simulated data source).
   - Include a diagram or brief write-up describing data flow and interactions.

2. **Frontend - Monitoring UI**
   - Build a web interface using React (or equivalent) that:
     - Displays a table/grid of devices with their status (e.g., online/offline, CPU usage %, temperature).
     - Allows sorting or filtering by device name or status.
     - Includes a details modal or page for each device.

3. **Backend - Simulated Data Feed**
   - Build an API backend using Flask, Node.js, or FastAPI.
   - Create endpoints like:
     - `GET /api/devices`  returns a list of devices and their latest stats
     - `GET /api/devices/:id`  returns detailed stats/history for a device
   - Simulate updates (e.g., random fluctuation of CPU usage, temperature) on request or on a timer.

4. **Bonus (Optional)**
   - Add charts for CPU and temperature over time using a library like Chart.js or Recharts.
   - Deploy the app using Railway, Vercel, or Netlify.

## >ê Deliverables

- Code (GitHub repo or zip file).
- A `README.md` with:
  - Setup instructions
  - System design overview
  - Screenshot or deployment link (if available)
- One-paragraph reflection on how youd expand the system (e.g., real-time WebSocket updates, authentication, alerting).

##  Evaluation Criteria

- Clear and usable interface
- Quality and modularity of code
- Cleanly simulated API behavior
- Documentation and presentation of your solution

---

**Tip:** You dont need real devices or sensors. Focus on system structure, dynamic data handling, and responsiveness in the UI.
