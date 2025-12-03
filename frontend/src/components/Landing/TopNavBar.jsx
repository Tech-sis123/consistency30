import React from 'react';
import { Link } from 'react-router-dom';

const TopNavBar = () => {
  return (
    <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-header-border-dark px-4 sm:px-10 py-3">
      <div className="flex items-center gap-4 text-white">
        <div className="size-6 text-primary">
          <span className="material-symbols-outlined !text-4xl">
            all_inclusive
          </span>
        </div>
        <h2 className="text-white text-lg font-bold leading-tight tracking-[-0.015em]">
          Consistency30
        </h2>
      </div>
      
      <div className="hidden md:flex flex-1 justify-end gap-8">
        <div className="flex items-center gap-9">
          <a className="text-white text-sm font-medium leading-normal hover:text-primary transition-colors" href="#">
            Features
          </a>
          <a className="text-white text-sm font-medium leading-normal hover:text-primary transition-colors" href="#">
            Pricing
          </a>
          <a className="text-white text-sm font-medium leading-normal hover:text-primary transition-colors" href="#">
            FAQ
          </a>
        </div>
        <div className="flex gap-2">
          <Link to='/login'>
          <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-secondary-button-dark text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-opacity-80 transition-colors">
            <span className="truncate">Log In</span>
          </button>
          </Link>
          <Link to='/register'>
          <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold leading-normal tracking-[0.015em] hover:bg-opacity-90 transition-colors">
            <span className="truncate">Start Your 30-Day Journey</span>
          </button>
          </Link>
        </div>
      </div>
      
      <div className="md:hidden">
        <button className="text-white">
          <span className="material-symbols-outlined !text-3xl">menu</span>
        </button>
      </div>
    </header>
  );
};

export default TopNavBar;