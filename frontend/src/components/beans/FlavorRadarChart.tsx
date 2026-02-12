"use client";

interface FlavorRadarChartProps {
  categories: { label: string; count: number }[];
  maxValue?: number;
}

export default function FlavorRadarChart({
  categories,
  maxValue,
}: FlavorRadarChartProps) {
  const max = maxValue || Math.max(...categories.map((c) => c.count), 1);
  const size = 200;
  const cx = size / 2;
  const cy = size / 2;
  const r = 80;
  const n = categories.length;

  if (n < 3) return null;

  const angleStep = (2 * Math.PI) / n;

  const getPoint = (index: number, value: number) => {
    const angle = angleStep * index - Math.PI / 2;
    const ratio = value / max;
    return {
      x: cx + r * ratio * Math.cos(angle),
      y: cy + r * ratio * Math.sin(angle),
    };
  };

  const dataPoints = categories.map((cat, i) => getPoint(i, cat.count));
  const dataPath = dataPoints
    .map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${p.y}`)
    .join(" ");

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="w-full max-w-[200px] mx-auto">
      {/* Grid circles */}
      {[0.25, 0.5, 0.75, 1].map((ratio) => (
        <circle
          key={ratio}
          cx={cx}
          cy={cy}
          r={r * ratio}
          fill="none"
          stroke="#e7e5e4"
          strokeWidth={0.5}
        />
      ))}

      {/* Grid lines */}
      {categories.map((_, i) => {
        const p = getPoint(i, max);
        return (
          <line
            key={i}
            x1={cx}
            y1={cy}
            x2={p.x}
            y2={p.y}
            stroke="#e7e5e4"
            strokeWidth={0.5}
          />
        );
      })}

      {/* Data polygon */}
      <path
        d={`${dataPath} Z`}
        fill="rgba(120, 53, 15, 0.15)"
        stroke="#78350f"
        strokeWidth={1.5}
      />

      {/* Data points */}
      {dataPoints.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={3} fill="#78350f" />
      ))}

      {/* Labels */}
      {categories.map((cat, i) => {
        const labelPoint = getPoint(i, max * 1.25);
        return (
          <text
            key={i}
            x={labelPoint.x}
            y={labelPoint.y}
            textAnchor="middle"
            dominantBaseline="central"
            className="text-[8px] fill-stone-600"
          >
            {cat.label}
          </text>
        );
      })}
    </svg>
  );
}
