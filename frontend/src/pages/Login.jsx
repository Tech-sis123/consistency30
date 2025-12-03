import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here
    console.log('Login attempt:', { email, password });
  };

  return (
    <div className="min-h-screen flex flex-col">
      <style jsx>{`
        .dark .form-input {
          background-color: #2D2D37;
          border-color: #3E3E4A;
          color: #EAEAEA;
        }
        .dark .form-input::placeholder {
          color: #8A8A93;
        }
        .dark .form-input:focus {
          border-color: #6A0DAD;
          box-shadow: 0 0 0 1px #6A0DAD;
        }
        .dark .eye-icon-container {
          background-color: #2D2D37;
          border-color: #3E3E4A;
        }
        .dark .eye-icon-container:focus-within {
          border-color: #6A0DAD;
          box-shadow: 0 0 0 1px #6A0DAD;
        }
        .dark .input-password:focus + .eye-icon {
          border-color: #6A0DAD;
        }
      `}</style>

      <div className="flex min-h-screen w-full flex-col items-center justify-center overflow-x-hidden p-4 sm:p-6 lg:p-8 bg-background-light dark:bg-background-dark font-display text-[#140d1b] dark:text-[#EAEAEA]">
        {/* Background Gradient */}
        <div className="absolute inset-0 z-0 h-full w-full bg-background-light dark:bg-background-dark dark:bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(42,13,58,0.3),rgba(255,255,255,0))]"></div>
        
        <div className="relative z-10 flex w-full max-w-md flex-col items-center">
          {/* Logo */}
          <Link to='/'>
          <div className="mb-8 flex items-center gap-3">
            <svg 
              className="h-8 w-8 text-primary" 
              fill="currentColor" 
              viewBox="0 0 24 24" 
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"></path>
            </svg>
            <span className="text-2xl font-bold tracking-tighter text-zinc-900 dark:text-white">
              Consistency30
            </span>
          </div>
          </Link>

          {/* Form Container */}
          <div className="w-full rounded-xl bg-white dark:bg-[#1C1C23] p-6 sm:p-8 shadow-lg">
            <div className="flex flex-col items-center text-center">
              <h1 className="text-3xl font-bold tracking-tight text-[#140d1b] dark:text-white">
                Welcome Back
              </h1>
              <p className="mt-2 text-base text-zinc-600 dark:text-[#EAEAEA]">
                Log in to your Consistency30 account
              </p>
            </div>

            <form onSubmit={handleSubmit} className="mt-8 flex flex-col gap-4">
              {/* Email Field */}
              <div className="flex flex-col">
                <label 
                  htmlFor="email" 
                  className="mb-2 text-base font-medium text-[#140d1b] dark:text-[#EAEAEA]"
                >
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="form-input h-14 w-full rounded-lg border border-[#dbcfe7] bg-[#faf8fc] p-4 text-base placeholder:text-[#734c9a] focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary dark:placeholder:text-[#8A8A93]"
                  required
                />
              </div>

              {/* Password Field */}
              <div className="flex flex-col">
                <label 
                  htmlFor="password" 
                  className="mb-2 text-base font-medium text-[#140d1b] dark:text-[#EAEAEA]"
                >
                  Password
                </label>
                <div className="relative flex w-full items-center">
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="form-input input-password h-14 w-full rounded-lg border border-[#dbcfe7] bg-[#faf8fc] p-4 pr-12 text-base placeholder:text-[#734c9a] focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary dark:placeholder:text-[#8A8A93]"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-0 top-0 flex h-14 w-12 items-center justify-center text-zinc-500 dark:text-[#8A8A93] hover:text-primary transition-colors"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    <span className="material-symbols-outlined">
                      {showPassword ? "visibility_off" : "visibility"}
                    </span>
                  </button>
                </div>
              </div>

              {/* Forgot Password Link */}
              <a 
                href="#" 
                className="self-end text-sm font-normal text-zinc-600 underline hover:text-primary dark:text-[#EAEAEA] dark:hover:text-primary transition-colors"
              >
                Forgot Password?
              </a>

              {/* Log In Button */}
              <button
                type="submit"
                className="mt-6 flex h-14 w-full items-center justify-center rounded-lg bg-primary text-base font-medium text-white transition-colors hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 dark:focus:ring-offset-background-dark"
              >
                Log In
              </button>
            </form>

            {/* Sign-Up Link */}
            <p className="mt-8 text-center text-sm text-zinc-600 dark:text-[#EAEAEA]">
              Don't have an account? 
              <Link 
                to="/register" 
                className="ml-1 font-bold text-primary hover:underline transition-colors"
              >
                Sign Up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;