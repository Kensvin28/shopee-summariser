const SentimentBar = ({ positive, neutral, negative }) => {
  const getProgressBarWidth = (value) => {
    return `${value}%`;
  };

  return (
    <div className="progress align-self-center h-100">
      <div
        className="progress-bar bg-success text-nowrap"
        role="progressbar"
        style={{ width: getProgressBarWidth(positive) }}
      >
        {positive}%
      </div>
      <div
        className="progress-bar bg-warning text-nowrap"
        role="progressbar"
        style={{ width: getProgressBarWidth(neutral) }}
      >
        {neutral}%
      </div>
      <div
        className="progress-bar bg-danger text-nowrap"
        role="progressbar"
        style={{ width: getProgressBarWidth(negative) }}
      >
        {negative}%
      </div>
    </div>
  );
};

export default SentimentBar;
