export default function RiskGauge({ score }) {
  const background = `conic-gradient(#ff6b6b 0 ${score}%, rgba(255,255,255,0.08) ${score}% 100%)`;

  return (
    <div style={{ display: "grid", placeItems: "center", margin: "20px 0" }}>
      <div
        style={{
          width: 150,
          height: 150,
          borderRadius: "50%",
          background,
          display: "grid",
          placeItems: "center"
        }}
      >
        <div
          style={{
            width: 110,
            height: 110,
            borderRadius: "50%",
            background: "#0d1e19",
            display: "grid",
            placeItems: "center",
            fontSize: 28,
            fontWeight: 700
          }}
        >
          {score}
        </div>
      </div>
    </div>
  );
}