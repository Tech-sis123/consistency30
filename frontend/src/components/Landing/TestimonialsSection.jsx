import React from 'react';
import AutoSlider from './AutoSlider';

const TestimonialsSection = () => {
  const testimonials = [
    {
      name: "Alex Johnson",
      role: "Software Engineer",
      quote: "Consistency30 completely changed my morning routine. The AI accountability partner is a game-changer!",
      imageUrl: "https://lh3.googleusercontent.com/aida-public/AB6AXuCJo2RdJEQdF01-J8I7Px-nVWJ3nVVXCY7mnQTzmtZ_mfKVEPC0GkNYDI1ABJQPZ8rboge2dJ3buZuRCa3Ywu68XpOQKnrNqFEbTibQbfc18kWyuOblm5548uuimAmTgbf01wRpfHrojPYX7kY1597lSZXDuJiip3VgKMJe-zF8fzvRMAz2xY0T9yk09JTms48eK3hQRs5ZNTGiNCZRaNIBEcgWEkWF_gmE1GrQl0wVUgbMj8FLcxVmlAxRKd1Xa9v4M2My1zykxCRJ"
    },
    {
      name: "Samantha Lee",
      role: "Graphic Designer",
      quote: "I've tried so many habit apps, but this is the first one that's actually stuck. Highly recommend for creative professionals.",
      imageUrl: "https://lh3.googleusercontent.com/aida-public/AB6AXuCJ7GkZDn6crHVqPa1IwyW0GEzfF1gwip7rwFMNMtsB9NQY1r8kbhbgtLAU9yhLQW-BqDOH5zHuCkNq06eOk0Mlr73Xcu2Iyr799BdqC4RrDyUfyzji7J12_arkctP4QBrn1JMMFNIv6-vZvVpt9ujbxcu5Q7xNUVfuIayhj9yrWFEeh2jMfJmvENRla8CVxh37dt3MiB3uKkyMRvAt62wP2akLLOqYPx4XD__8yg-HdOeCTZTQ55E-gNDll_fHFr0OnI9cOavrsYIK"
    },
    {
      name: "Michael Chen",
      role: "Student",
      quote: "The gamified approach makes building habits fun instead of a chore. I finally hit a 30-day streak for studying!",
      imageUrl: "https://lh3.googleusercontent.com/aida-public/AB6AXuDX9SB1uQH2ILaqeXTVO5VtSvkO-NI_rGLHfyd39VmxUBFKRNgs-4s8BxyR3fa8jXdGTTsmEZmUAQY4vItxGTbvZ96U4L-HVKygZZC505lVE2LwcnIyV_C8MPVf2F1j14gwgB-SUule7snZhh8Dv0wRRaErSxUppBTS_Raclk1W-qtV8BAo8H2qI21RABOqGeBjjIm5wvIQDwVF16fE4L-ENDab_1fUyW2FH7FDKPuNUeEyfGLrqspxmjQBH4gl9xq7Kmc3cPccUUOn"
    },
    {
      name: "Emily Carter",
      role: "Entrepreneur",
      quote: "As a founder, my schedule is chaotic. This app brought much-needed structure and consistency to my life.",
      imageUrl: "https://lh3.googleusercontent.com/aida-public/AB6AXuC7UqtWA0G2YRp0dvRlCmKhJzi8qpgeQQVFlUulj45o-147Oszyg8GqU-YfPwx3t34QyF5bckBMawf-68NW7SenEi2s9Zw5BMpP3QUdTwpFFQbzPF-8qjl6PPqENm-u_n7aMh2moi6MIA8Q2mmAIGsemjWro_w7HtWUU3ttIn2DrbEZwjFPB4r2_G-B9XvXn7UPKml4DRCNqPt6vMt29nkc-4YZD_Vv8UhZ8OtQjtobas8Ps1XeW0iSkP-Ix2S4YtCNrabjjPH1WQsz"
    },
    {
      name: "David Wilson",
      role: "Fitness Coach",
      quote: "This app helped me maintain consistency in my training. The AI accountability is like having a personal trainer 24/7!",
      imageUrl: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop"
    },
    {
      name: "Sarah Martinez",
      role: "Writer",
      quote: "As a writer, discipline is everything. Consistency30 helped me write 500 words every day for 30 days straight!",
      imageUrl: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w-400&h=400&fit=crop"
    }
  ];

  return (
    <section className="px-4">
      <div className="flex flex-col items-center text-center mb-8">
        <h2 className="text-white text-[28px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
          Join thousands of successful users
        </h2>
        <p className="text-text-muted-dark max-w-xl">
          Hear from our community members who transformed their lives with Consistency30
        </p>
      </div>
      
      <AutoSlider testimonials={testimonials} autoSlideInterval={1500} />
    </section>
  );
};

export default TestimonialsSection;