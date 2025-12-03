import React from 'react';

const TestimonialCard = ({ name, role, quote, imageUrl }) => {
  return (
    <div className="flex h-full flex-1 flex-col gap-4 rounded-xl min-w-72 bg-card-dark p-6 border border-card-border-dark">
      <div className="flex items-center gap-4">
        <div 
          className="w-12 h-12 bg-center bg-no-repeat aspect-square bg-cover rounded-full flex flex-col"
          style={{ backgroundImage: `url("${imageUrl}")` }}
          alt={`Portrait of ${name}`}
        />
        <div>
          <p className="text-white text-base font-medium leading-normal">{name}</p>
          <p className="text-text-muted-dark text-sm font-normal leading-normal">{role}</p>
        </div>
      </div>
      <p className="text-text-muted-dark text-sm font-normal leading-normal">
        "{quote}"
      </p>
    </div>
  );
};

export default TestimonialCard;