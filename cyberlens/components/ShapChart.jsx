export default function ShapChart({ modules }) {
  return (
    <div>
      <h3>Phase Contributions</h3>
      {modules.map((module) => (
        <div key={module.module || "module"} style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <span>{(module.module || "module").toUpperCase()}</span>
            <span>{module.score || 0}</span>
          </div>
          <div style={{ height: 10, background: "rgba(255,255,255,0.08)", borderRadius: 999 }}>
            <div
              style={{
                height: "100%",
                width: `${Math.min(module.score || 0, 100)}%`,
                background: "linear-gradient(90deg, #8ef0b5, #ffd166)",
                borderRadius: 999
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}