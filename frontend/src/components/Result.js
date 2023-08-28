import "bootstrap/dist/css/bootstrap.css";
import Feature from "./Feature";
import Legend from "./Legend";
import OverallChart from "./OverallChart";
import Links from "./Links";

const Result = (props) => {
  return (
    <div>
      <div className="d-flex flex-row w-100 justify-content-between">
        <div className="w-75 card d-flex flex-col mb-2 rounded-1">
          <div className="px-2 py-1 fw-bold">{props.title}</div>
          <div className="px-2 py-1 d-flex flex-row">
            <div className="w-75 align-items-center d-flex">
              ⭐ {props.rating} out of {props.total_reviews} reviews
            </div>
          </div>
          <Links aspect_sentiment={props.aspect_sentiment} />
        </div>
        <div className="w-25 card mb-2 rounded-1 d-flex flex-row justify-content-center align-items-center">
          <OverallChart
            positive={parseFloat(props.overall_sentiment.positive)}
            neutral={parseFloat(props.overall_sentiment.neutral)}
            negative={parseFloat(props.overall_sentiment.negative)}
          />
        </div>
      </div>
      <Legend />
      {props.aspect_sentiment?.map((feature) => (
        <Feature feature={feature}></Feature>
      ))}
    </div>
  );
};

export default Result;
