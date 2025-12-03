import React, { useState, useEffect, useRef } from 'react';
import TestimonialCard from './TestimonialCard';

const AutoSlider = ({ testimonials, autoSlideInterval = 1500 }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const sliderRef = useRef(null);

  const goToSlide = (index) => {
    if (sliderRef.current) {
      const container = sliderRef.current;
      const card = container.querySelector('.testimonial-card');
      if (card) {
        const cardWidth = card.offsetWidth + 16; // card width + gap
        container.scrollTo({
          left: index * cardWidth,
          behavior: 'smooth'
        });
      }
    }
    setCurrentIndex(index);
  };

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === testimonials.length - 1 ? 0 : prevIndex + 1
    );
  };

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => 
      prevIndex === 0 ? testimonials.length - 1 : prevIndex - 1
    );
  };

  // Auto slide effect
  useEffect(() => {
    if (!isPaused) {
      const interval = setInterval(() => {
        nextSlide();
      }, autoSlideInterval);

      return () => clearInterval(interval);
    }
  }, [isPaused, currentIndex, autoSlideInterval]);

  // Scroll to current slide when index changes
  useEffect(() => {
    if (sliderRef.current) {
      const container = sliderRef.current;
      const card = container.querySelector('.testimonial-card');
      if (card) {
        const cardWidth = card.offsetWidth + 16; // card width + gap
        container.scrollTo({
          left: currentIndex * cardWidth,
          behavior: 'smooth'
        });
      }
    }
  }, [currentIndex]);

  return (
    <div className="relative">
      {/* Slider container */}
      <div 
        ref={sliderRef}
        className="flex overflow-x-auto [-ms-scrollbar-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden py-8 scroll-smooth"
        onMouseEnter={() => setIsPaused(true)}
        onMouseLeave={() => setIsPaused(false)}
      >
        <div className="flex items-stretch p-4 gap-4 w-max">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="testimonial-card">
              <TestimonialCard
                name={testimonial.name}
                role={testimonial.role}
                quote={testimonial.quote}
                imageUrl={testimonial.imageUrl}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Navigation dots */}
      <div className="flex justify-center gap-2 mt-4">
        {testimonials.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`w-2 h-2 rounded-full transition-all duration-300 ${
              index === currentIndex 
                ? 'bg-primary w-6' 
                : 'bg-card-border-dark hover:bg-primary/50'
            }`}
            aria-label={`Go to testimonial ${index + 1}`}
          />
        ))}
      </div>

      {/* Navigation arrows for desktop */}
      <div className="hidden md:block">
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-card-dark/80 hover:bg-card-dark text-white p-2 rounded-full hover:scale-110 transition-all"
          aria-label="Previous testimonial"
        >
          <span className="material-symbols-outlined">chevron_left</span>
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-card-dark/80 hover:bg-card-dark text-white p-2 rounded-full hover:scale-110 transition-all"
          aria-label="Next testimonial"
        >
          <span className="material-symbols-outlined">chevron_right</span>
        </button>
      </div>

      {/* Auto-play indicator */}
      <div className="text-center mt-2">
        <span className="text-text-muted-dark text-sm flex items-center justify-center gap-1">
        </span>
      </div>
    </div>
  );
};

export default AutoSlider;