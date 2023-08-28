import React, { useState } from "react";
import InputBar from "./components/InputBar";
import Result from "./components/Result";
import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";

const App = () => {
  const [productURL, setURL] = useState("");
  const [error, setError] = useState({});
  const [response, setResponse] = useState({ rating: null, sentiment: null, sentiment_probs: null });
  const [display, setDisplay] = useState(false);
  const [submit, setSubmit] = useState(false);
  const [title, setTitle] = useState("");
  const SERVER = "http://127.0.0.1:5000/"

  const handleURL = (event) => {
    setURL(event.target.value);
  };
  const controller = new AbortController();

  const getSummary = async (event) => {
    setDisplay(false);
    // reset error
    setError({});
    // prevent refresh when submitting
    event.preventDefault();
    controller.abort();
    // validate URL
    if (productURL.includes("shopee.com.my/")) {
      setSubmit(true);
      // send request
      const response = await axios.post(SERVER, {
        data: productURL, signal: controller.signal
      });
      setResponse(response);
      if(response.data.hasOwnProperty("error")){
        setDisplay(false);
      } else {
        setDisplay(true);
      }
      console.log(response.data);
      // set title from URL
      const titleWithHyphens = productURL.match(/\/([^/]+)\-i\.\d+\.\d+\?/)[1];
      setTitle(titleWithHyphens.replace(/-/g, " "));
      setSubmit(false);
      setDisplay(true);
    }

    // if URL is not found or invalid
    else {
      setError({ type: "URL Invalid" });
    }
  };

  return (
    <div className="flex-col justify-content-center mx-4 my-3">
        <h1 className="fs-2">Product Review Summariser</h1>
        <form onSubmit={getSummary}>
          <InputBar value={productURL} onChange={handleURL} error={error}></InputBar>
        </form>
        <div>{response.error}</div>
        {submit && (
          // Loading animation
          <img className="py-5"
            src="https://raw.githubusercontent.com/Codelessly/FlutterLoadingGIFs/master/packages/cupertino_activity_indicator_large.gif"
            alt="Loading..."
          ></img>
        )}
        {display && (
            <Result
              title={title}
              rating={response.data.overall_rating}
              sentiment={response.data.sentiment}
              total_reviews={response.data.total_reviews}
              features={response.data.features}
              aspect_sentiment={response.data.aspect_sentiment}
              overall_sentiment={response.data.overall_sentiment}
            ></Result>
        )}
      </div>
  );
};

export default App;
