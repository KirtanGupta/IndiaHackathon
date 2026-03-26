export default function RiskGauge({ score }) {
  const background = `conic-gradient(#ff3b30 0 ${score}%, #8a101a ${score}% 68%, rgba(255,255,255,0.08) 68% 100%)`;

  return (
    <div style={{ display: "grid", placeItems: "center", margin: "22px 0" }}>
      <div
        style={{
          width: 158,
          height: 158,
          borderRadius: "50%",
          background,
          display: "grid",
          placeItems: "center",
          boxShadow: "0 24px 50px rgba(0, 0, 0, 0.42)",
        }}
      >
        <div
          style={{
            width: 116,
            height: 116,
            borderRadius: "50%",
            background: "radial-gradient(circle at top, #190709 0%, #070303 100%)",
            border: "1px solid rgba(255,255,255,0.06)",
            display: "grid",
            placeItems: "center",
            fontSize: 30,
            fontWeight: 800,
            color: "#fff1f1",
          }}
        >
          {score}
        </div>
      </div>
    </div>
  );
}
