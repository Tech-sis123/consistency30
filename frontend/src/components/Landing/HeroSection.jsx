import React from 'react';

const HeroSection = () => {
  return (
    <section className="@container py-10 sm:py-20">
      <div className="@[480px]:p-4">
        <div 
          className="flex min-h-[480px] flex-col gap-6 bg-cover bg-center bg-no-repeat @[480px]:gap-8 items-center justify-center p-4"
          style={{ backgroundImage: 'radial-gradient(circle, rgba(126, 86, 245, 0.1) 0%, rgba(20, 16, 34, 0.1) 70%)' }}
        >
          <div className="relative mb-4">
            <div className="w-32 h-32 rounded-full bg-primary/20 flex items-center justify-center">
              <div className="w-24 h-24 rounded-full bg-primary/40 flex items-center justify-center">
                <span className="material-symbols-outlined !text-6xl text-primary animate-pulse">
                  psychology
                </span>
              </div>
            </div>
          </div>
          
          <div className="flex flex-col gap-2 text-center max-w-2xl">
            <h1 className="text-white text-4xl font-black leading-tight tracking-[-0.033em] @[480px]:text-5xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em]">
              Build lasting habits with AI accountability
            </h1>
            <h2 className="text-text-muted-dark text-base font-normal leading-normal @[480px]:text-lg @[480px]:font-normal @[480px]:leading-normal">
              Your personal AI partner will guide you through our proven 30-day challenge to help you achieve your goals and build habits that stick.
            </h2>
          </div>
          
          <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 @[480px]:h-12 @[480px]:px-6 bg-primary text-white text-base font-bold leading-normal tracking-[0.015em] hover:bg-opacity-90 transition-transform transform hover:scale-105">
            <span className="truncate">Start Your 30-Day Journey</span>
          </button>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;