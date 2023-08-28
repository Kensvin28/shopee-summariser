import React from 'react'

const Links = (props) => {
  return (
    <div>
      <div className="py-1"></div>
      <div className="card-group d-flex flex-row">
        {props.aspect_sentiment?.map((feature, index) => (
          <div className="p-1 py-0" key={index}>
            <div className="p-1">
              <a
                href={`#${feature.name}`}
                className="card-link btn btn-light btn-sm border"
              >
                {feature.name}
              </a>
            </div>
          </div>
        ))}
      </div>
      <div className="py-1"></div>
    </div>
  );
}

export default Links;