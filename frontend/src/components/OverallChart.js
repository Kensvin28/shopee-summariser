import "chart.js/auto";
import { Doughnut } from "react-chartjs-2";
import ChartDataLabels from "chartjs-plugin-datalabels";

const OverallChart = ({positive, neutral, negative}) => {
  let text;
  // Classify overall sentiment
  if (positive > neutral && positive > negative) {
    text = "Positive";
  } else if (neutral > positive && neutral > negative) {
    text = "Neutral";
  } else {
    text = "Negative";
  }

  // Data for chart
  const data = {
    labels: ["Positive", "Neutral", "Negative"],
    datasets: [
      {
        data: [positive, neutral, negative],
        backgroundColor: [
          "rgba(25, 135, 84, 1)",
          "rgba(255, 193, 7, 1)",
          "rgba(220, 53, 69, 1)",
        ],
      },
    ],
  };

  // Styling
  const options = {
    plugins: {
      legend: {
        display: false,
      },
      datalabels: {
        formatter: (value) => {
          return `${value}%`; // Add percentage sign
        },
        display: function(context) {
          var index = context.dataIndex;
          var value = context.dataset.data[index];
          return value < 5 ? 'auto' : true;
        },
        anchor: "end", // Position the labels at the end of the arc
        align: "end", // Align the labels at the end of the arc
        offset: -5, // Set the offset distance from the arc (in pixels)
        clamp: true, // Prevent labels from overlapping the chart
      },
    },
    cutout: "50%", // hollow size
    maintainAspectRatio: false,
    layout: {
      padding: {
        top: 10,
        bottom: 10,
      },
    },
  };

  return (
    <div className="w-100 h-100">
      <div className="py-1 text-center fw-bold">Overall sentiment</div>
      <div className="py-2">
        <Doughnut
          data={data}
          options={options}
          plugins={[ChartDataLabels]}
          height={100}
          width={100}
        />
      </div>
      <div className="text-center pb-1">{text}</div>
    </div>
  );
};

export default OverallChart;
