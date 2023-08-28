const Review = (props) => {
    return (
      <div className="border-top nav-item">
        <div className="px-3 py-2">{props.comment}</div>
      </div>
    );
}

export default Review;