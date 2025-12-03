import React from 'react';

const CTASection = () => {
  return (
    <section className="bg-card-dark border border-card-border-dark rounded-xl my-10 p-8 sm:p-12 text-center flex flex-col items-center gap-6">
      <h2 className="text-white text-3xl font-bold leading-tight tracking-[-0.015em] max-w-lg">
        Ready to build habits that last a lifetime?
      </h2>
      <p className="text-text-muted-dark text-base font-normal leading-normal max-w-xl">
        Stop wishing and start doing. Your AI partner is ready to guide you, one day at a time. Your future self will thank you.
      </p>
      <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-6 bg-primary text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-opacity-90 transition-transform transform hover:scale-105">
        <span className="truncate">Start Your 30-Day Journey Now</span>
      </button>
    </section>
  );
};

export default CTASection;