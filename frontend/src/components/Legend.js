import React from "react";

const Legend = () => {
  return (
    <div className="legend mb-2 d-flex flex-row justify-content-end">
      <div>
        <span
          className="label positive"
          style={{
            color: "transparent",
            fontSize: 12,
            textShadow: "0 0 0 rgba(40, 167, 69, 1)",
          }}
        >
          🟢
        </span>
        <span style={{ fontSize: 12 }}>Positive</span>
      </div>
      <div className="px-2">
        <span
          className="label neutral"
          style={{
            color: "transparent",
            fontSize: 12,
            textShadow: "0 0 0 rgba(255, 193, 7, 1)",
          }}
        >
          🟡
        </span>
        <span style={{ fontSize: 12 }}>Neutral</span>
      </div>
      <div>
        <span
          className="label negative"
          style={{
            color: "transparent",
            fontSize: 12,
            textShadow: "0 0 0 rgba(220, 53, 69, 1)",
          }}
        >
          🔴
        </span>
        <span style={{ fontSize: 12 }}>Negative</span>
      </div>
    </div>
  );
};

export default Legend;
