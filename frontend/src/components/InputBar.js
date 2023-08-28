import React from "react";

const InputBar = (props) => {
  return (
    <div className="mb-2">
      <div className="bg-opacity-10">Shopee Malaysia Product URL:</div>
      <div className="d-flex flex-row align-items-center">
        <input
          type="text"
          placeholder="Enter product URL to be summarised"
          value={props.value}
          onChange={props.onChange}
          className="w-100 h-100"
        />
        <button type="submit" className="btn btn-primary ms-2">
          Generate
        </button>
      </div>
      {props.error && <p className="text-danger my-0">{props.error.type}</p>}
    </div>
  );
};

export default InputBar;
