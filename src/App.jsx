import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [view, setView] = useState("table");

useEffect(() => {
    fetch("http://13.220.133.123/patients_html.py")
      .then((res) => res.json())
      .then((data) => {
        setEquipment(data.equipment)
        setLoading(false)
      })
      .catch((err) => {
        setError("Error loading data.");
        setLoading(false)
      });
  }, []);

  const total = equipment.length
  const due = equipment.filter((e) => e.status === "Due soon").length;
  const repair = equipment.filter((e) => e.status === "Needs repair").length

  //function for badge color
  const getBadgeClass = (status) => {
    if (status === "Operational") return "badge-ok"
    if (status === "Due soon") return "badge-warn"
    return "badge-err"
  }

  return (
    <div>
      <div className="header">
        <div className="header-logo">GE</div>
        <div>
          <div className="header-title">GE Healthcare Equipment Maintenance</div>
          <div className="header-sub">Imaging device tracker</div>
        </div>
        <div className="nav">
          <button onClick={() => setView("table")} className={view === "table" ? "active" : ""}>Dashboard</button>
          <button onClick={() => setView("api")} className={view === "api" ? "active" : ""}>Raw JSON</button>
        </div>
      </div>

      <div className="main">

      {view === "table" && (
          <>
            <div className="stats">
              <div className="stat">
                <div className="stat-label">Total Equipment</div>
                <div className="stat-value">{loading ? "-" : total}</div>
              </div>
              <div className="stat">
                <div className="stat-label">Due for Maintenance</div>
                <div className="stat-value stat-warn">{loading ? "-" : due}</div>
              </div>
              <div className="stat">
                <div className="stat-label">Needs Repair</div>
                <div className="stat-value stat-danger">{loading ? "-" : repair}</div>
              </div>
            </div>

            <div className="section-title">Maintenance Records</div>
            <div className="table-wrapper">
              {loading && <p className="loading">Loading...</p>}
              {error && <p className="error">{error}</p>}
              {!loading && !error && (
                <table>
                  <thead>
                    <tr>
                      <th>Equipment ID</th>
                      <th>Type</th>
                      <th>Location</th>
                      <th>Last Maintenance</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {equipment.map((item) => (
                      <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.type}</td>
                        <td>{item.location}</td>
                        <td>{item.last_maintenance}</td>
                        <td><span className={`badge ${getBadgeClass(item.status)}`}>{item.status}</span></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </>
        )}

        {view === "api" && (
          <>
          <div className="section-title">Raw API Response</div>
            <div className="code-wrapper">
              {loading && <p style={{color: "#d4d4d4"}}>Loading...</p>}
              {error && <p style={{color: "red"}}>{error}</p>}
              {!loading && !error && (
                <pre>{JSON.stringify({status: "success", total_records: total, equipment}, null, 2)}</pre>
              )}
            </div>
          </>
        )}

      </div>
    </div>
  );
}

export default App;