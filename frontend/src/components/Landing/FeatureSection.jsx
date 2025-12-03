import React from 'react';

const FeatureCard = ({ icon, title, description }) => {
  return (
    <div className="flex flex-1 gap-4 rounded-xl border border-card-border-dark bg-card-dark p-6 flex-col">
      <div className="text-primary" data-size="24px" data-weight="regular">
        <span className="material-symbols-outlined !text-3xl">{icon}</span>
      </div>
      <div className="flex flex-col gap-1">
        <h3 className="text-white text-lg font-bold leading-tight">{title}</h3>
        <p className="text-text-muted-dark text-sm font-normal leading-normal">
          {description}
        </p>
      </div>
    </div>
  );
};

const FeatureSection = () => {
  const features = [
    {
      icon: "smart_toy",
      title: "AI-Powered Accountability",
      description: "Chat with your intelligent AI partner who keeps you motivated and on track with daily check-ins and support."
    },
    {
      icon: "trending_up",
      title: "Gamified Progress Tracking",
      description: "Maintain streaks, earn points, and unlock rewards as you consistently complete your habits."
    },
    {
      icon: "rule",
      title: "Personalized Habit Plans",
      description: "Set and customize your habit goals with guidance from your AI to ensure they are achievable and effective."
    }
  ];

  return (
    <section className="flex flex-col gap-10 px-4 py-10 @container">
      <div className="flex flex-col gap-4 text-center items-center">
        <h2 className="text-white tracking-light text-[32px] font-bold leading-tight @[480px]:text-4xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em] max-w-[720px]">
          How Consistency30 Works
        </h2>
        <p className="text-text-muted-dark text-base font-normal leading-normal max-w-[720px]">
          We combine behavioral science with cutting-edge AI to provide a personalized and gamified habit-building experience.
        </p>
      </div>
      
      <div className="grid grid-cols-[repeat(auto-fit,minmax(240px,1fr))] gap-4 p-0">
        {features.map((feature, index) => (
          <FeatureCard
            key={index}
            icon={feature.icon}
            title={feature.title}
            description={feature.description}
          />
        ))}
      </div>
    </section>
  );
};

export default FeatureSection;