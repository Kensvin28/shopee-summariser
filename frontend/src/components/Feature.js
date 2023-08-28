import "bootstrap/dist/css/bootstrap.css";
import { useState } from "react";
import Review from "./Review";
import SentimentBar from "./SentimentBar";

const Feature = (props) => {
  const [showReview, setShowReview] = useState(false);
  const [showAllReviews, setShowAllReviews] = useState(false);
  const [selectedSentiment, setSelectedSentiment] = useState("positive");

  const feature = props.feature;
  const handleClick = () => {
    setShowReview(!showReview);
    setShowAllReviews(!showAllReviews);
  };
  // concatenate opinions
  const opinions = feature.opinions?.map((item) => item).join(", ");

  const handleTabClick = (tab) => {
    setSelectedSentiment(tab);
  };

  return (
    <div id={feature.name} className="card rounded-1">
      <div
        className="card-header d-flex fw-semibold"
        onClick={handleClick}
        type="button"
      >
        <div className="w-25">
          <span>{`${feature.name}: ${opinions}`}</span>
        </div>
        <div className="w-50">
          <SentimentBar
            positive={feature.sentiments.positive}
            neutral={feature.sentiments.neutral}
            negative={feature.sentiments.negative}
          ></SentimentBar>
        </div>
        {/* arrow */}
        <div className="w-25 d-flex flex-row-reverse">
          <svg
            className="mt-1"
            width="16"
            height="16"
            type="button"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
          >
            {showReview && (
              <path
                d="M233.4 406.6c12.5 12.5 32.8 12.5 45.3 0l192-192c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L256 338.7 86.6 169.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l192 192z"
                fill="black"
              />
            )}
            {!showReview && (
              <path
                d="M310.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-192 192c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L242.7 256 73.4 86.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l192 192z"
                fill="black"
              />
            )}
          </svg>
        </div>
      </div>
      <nav className="nav nav-tabs" role="tablist">
        {Object.keys(feature.reviews)
          .sort((a, b) => b.localeCompare(a))
          .map((sentiment) => (
            <div
              key={sentiment}
              className={`nav-item`}
              onClick={() => handleTabClick(sentiment)}
              role="button"
            >
              <div
                className={`${
                  selectedSentiment === sentiment ? "active" : ""
                } nav-link`}
              >
                {sentiment.charAt(0).toUpperCase() +
                  sentiment.slice(1) +
                  " (" +
                  feature.reviews[sentiment].length +
                  ")"}
              </div>
            </div>
          ))}
      </nav>
      <div className="tab-content">
        {showAllReviews
          ? feature.reviews[selectedSentiment].map((comment, index) => (
              <Review key={index} comment={comment} />
            ))
          : feature.reviews[selectedSentiment]
              .slice(0, 5)
              .map((comment, index) => (
                <Review key={index} comment={comment} />
              ))}
        {!showAllReviews && feature.reviews[selectedSentiment].length > 5 ? (
          <button
            className="btn btn-link text-decoration-none"
            onClick={handleClick}
          >
            Read More
          </button>
        ) : feature.reviews[selectedSentiment].length > 5 ? (
          <button
            className="btn btn-link text-decoration-none"
            onClick={handleClick}
          >
            Hide
          </button>
        ) : feature.reviews[selectedSentiment].length === 0 ? (
          <Review comment={"No review"} />
        ) : (
          <></>
        )}
      </div>
    </div>
  );
};

export default Feature;
