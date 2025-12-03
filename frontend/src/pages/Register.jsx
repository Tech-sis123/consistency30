import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validation
    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    
    if (formData.password.length < 6) {
      alert('Password must be at least 6 characters long');
      return;
    }
    
    // Here you would call your registration API
    console.log('Registration data:', formData);
    
    // Redirect to login or dashboard
    // window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark font-display text-gray-800 dark:text-gray-200">
      {/* Top Navigation Bar */}
      <header className="absolute top-0 left-0 right-0 z-10 p-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-7xl">
          <nav className="flex items-center justify-between">
            <Link to='/'>
            <div className="flex items-center gap-3 text-[#140d1b] dark:text-white">
              <div className="size-6 text-primary">
                <svg 
                  fill="none" 
                  viewBox="0 0 48 48" 
                  xmlns="http://www.w3.org/2000/svg"
                  className="w-6 h-6"
                >
                  <g clipPath="url(#clip0_6_543)">
                    <path d="M42.1739 20.1739L27.8261 5.82609C29.1366 7.13663 28.3989 10.1876 26.2002 13.7654C24.8538 15.9564 22.9595 18.3449 20.6522 20.6522C18.3449 22.9595 15.9564 24.8538 13.7654 26.2002C10.1876 28.3989 7.13663 29.1366 5.82609 27.8261L20.1739 42.1739C21.4845 43.4845 24.5355 42.7467 28.1133 40.548C30.3042 39.2016 32.6927 37.3073 35 35C37.3073 32.6927 39.2016 30.3042 40.548 28.1133C42.7467 24.5355 43.4845 21.4845 42.1739 20.1739Z" fill="currentColor"></path>
                    <path fillRule="evenodd" clipRule="evenodd" d="M7.24189 26.4066C7.31369 26.4411 7.64204 26.5637 8.52504 26.3738C9.59462 26.1438 11.0343 25.5311 12.7183 24.4963C14.7583 23.2426 17.0256 21.4503 19.238 19.238C21.4503 17.0256 23.2426 14.7583 24.4963 12.7183C25.5311 11.0343 26.1438 9.59463 26.3738 8.52504C26.5637 7.64204 26.4411 7.31369 26.4066 7.24189C26.345 7.21246 26.143 7.14535 25.6664 7.1918C24.9745 7.25925 23.9954 7.5498 22.7699 8.14278C20.3369 9.32007 17.3369 11.4915 14.4142 14.4142C11.4915 17.3369 9.32007 20.3369 8.14278 22.7699C7.5498 23.9954 7.25925 24.9745 7.1918 25.6664C7.14534 26.143 7.21246 26.345 7.24189 26.4066ZM29.9001 10.7285C29.4519 12.0322 28.7617 13.4172 27.9042 14.8126C26.465 17.1544 24.4686 19.6641 22.0664 22.0664C19.6641 24.4686 17.1544 26.465 14.8126 27.9042C13.4172 28.7617 12.0322 29.4519 10.7285 29.9001L21.5754 40.747C21.6001 40.7606 21.8995 40.931 22.8729 40.7217C23.9424 40.4916 25.3821 39.879 27.0661 38.8441C29.1062 37.5904 31.3734 35.7982 33.5858 33.5858C35.7982 31.3734 37.5904 29.1062 38.8441 27.0661C39.879 25.3821 40.4916 23.9425 40.7216 22.8729C40.931 21.8995 40.7606 21.6001 40.747 21.5754L29.9001 10.7285ZM29.2403 4.41187L43.5881 18.7597C44.9757 20.1473 44.9743 22.1235 44.6322 23.7139C44.2714 25.3919 43.4158 27.2666 42.252 29.1604C40.8128 31.5022 38.8165 34.012 36.4142 36.4142C34.012 38.8165 31.5022 40.8128 29.1604 42.252C27.2666 43.4158 25.3919 44.2714 23.7139 44.6322C22.1235 44.9743 20.1473 44.9757 18.7597 43.5881L4.41187 29.2403C3.29027 28.1187 3.08209 26.5973 3.21067 25.2783C3.34099 23.9415 3.8369 22.4852 4.54214 21.0277C5.96129 18.0948 8.43335 14.7382 11.5858 11.5858C14.7382 8.43335 18.0948 5.9613 21.0277 4.54214C22.4852 3.8369 23.9415 3.34099 25.2783 3.21067C26.5973 3.08209 28.1187 3.29028 29.2403 4.41187Z" fill="currentColor"></path>
                  </g>
                  <defs>
                    <clipPath id="clip0_6_543">
                      <rect fill="white" height="48" width="48"></rect>
                    </clipPath>
                  </defs>
                </svg>
              </div>
              <h2 className="text-lg font-bold tracking-tight">Consistency30</h2>
            </div>
            </Link>
            <div className="flex items-center gap-4">
              <a 
                className="text-[#140d1b] dark:text-white text-sm font-medium leading-normal hover:text-primary dark:hover:text-primary transition-colors" 
                href="/login"
              >
                Log In
              </a>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-1 items-center justify-center py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-16 items-center">
            {/* Left Column: Branding/Visual - Hidden on mobile, visible on lg+ */}
            <div className="hidden lg:flex flex-col items-center justify-center text-center p-8">
              <img 
                className="w-full max-w-md h-auto rounded-xl mb-8 object-cover shadow-lg"
                src="https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&auto=format&fit=crop"
                alt="Abstract 3D render of purple and pink glowing geometric shapes on a dark background"
              />
              <h1 className="text-3xl md:text-4xl font-bold text-[#140d1b] dark:text-white mb-4">
                Unlock Your Potential.
              </h1>
              <p className="text-lg text-gray-600 dark:text-gray-400 max-w-md">
                Build habits that last. One day at a time.
              </p>
            </div>

            {/* Right Column: Sign-Up Form */}
            <div className="w-full max-w-md mx-auto lg:max-w-lg">
              <div className="bg-white dark:bg-background-dark/50 p-6 sm:p-8 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700">
                <div className="mb-6 sm:mb-8 text-center lg:text-left">
                  <h1 className="text-2xl sm:text-3xl font-bold text-[#140d1b] dark:text-white leading-tight">
                    Create Your Account
                  </h1>
                  <p className="text-gray-600 dark:text-gray-400 mt-2 text-sm sm:text-base">
                    Start your 30-day journey to consistency
                  </p>
                </div>

                <form className="flex flex-col gap-4 sm:gap-6" onSubmit={handleSubmit}>
                  {/* Full Name */}
                  <div className="flex flex-col">
                    <label 
                      htmlFor="fullName" 
                      className="text-[#140d1b] dark:text-gray-200 text-sm font-medium leading-normal pb-2"
                    >
                      Full Name
                    </label>
                    <input
                      id="fullName"
                      name="fullName"
                      type="text"
                      value={formData.fullName}
                      onChange={handleChange}
                      placeholder="Enter your full name"
                      className="form-input w-full rounded-lg text-[#140d1b] dark:text-white focus:outline-0 border border-gray-300 dark:border-gray-600 bg-background-light dark:bg-background-dark h-12 sm:h-14 placeholder:text-gray-500 dark:placeholder:text-gray-400 p-3 sm:p-4 text-base font-normal leading-normal focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors"
                      required
                    />
                  </div>

                  {/* Email */}
                  <div className="flex flex-col">
                    <label 
                      htmlFor="email" 
                      className="text-[#140d1b] dark:text-gray-200 text-sm font-medium leading-normal pb-2"
                    >
                      Email Address
                    </label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Enter your email"
                      className="form-input w-full rounded-lg text-[#140d1b] dark:text-white focus:outline-0 border border-gray-300 dark:border-gray-600 bg-background-light dark:bg-background-dark h-12 sm:h-14 placeholder:text-gray-500 dark:placeholder:text-gray-400 p-3 sm:p-4 text-base font-normal leading-normal focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors"
                      required
                    />
                  </div>

                  {/* Password */}
                  <div className="flex flex-col">
                    <label 
                      htmlFor="password" 
                      className="text-[#140d1b] dark:text-gray-200 text-sm font-medium leading-normal pb-2"
                    >
                      Password
                    </label>
                    <div className="relative">
                      <input
                        id="password"
                        name="password"
                        type={showPassword ? "text" : "password"}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Create a password (min. 6 characters)"
                        className="form-input w-full rounded-lg text-[#140d1b] dark:text-white focus:outline-0 border border-gray-300 dark:border-gray-600 bg-background-light dark:bg-background-dark h-12 sm:h-14 placeholder:text-gray-500 dark:placeholder:text-gray-400 p-3 sm:p-4 pr-12 text-base font-normal leading-normal focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors"
                        required
                        minLength="6"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-primary transition-colors"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                      >
                        <span className="material-symbols-outlined text-xl">
                          {showPassword ? "visibility_off" : "visibility"}
                        </span>
                      </button>
                    </div>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      Must be at least 6 characters long
                    </p>
                  </div>

                  {/* Confirm Password */}
                  <div className="flex flex-col">
                    <label 
                      htmlFor="confirmPassword" 
                      className="text-[#140d1b] dark:text-gray-200 text-sm font-medium leading-normal pb-2"
                    >
                      Confirm Password
                    </label>
                    <div className="relative">
                      <input
                        id="confirmPassword"
                        name="confirmPassword"
                        type={showConfirmPassword ? "text" : "password"}
                        value={formData.confirmPassword}
                        onChange={handleChange}
                        placeholder="Confirm your password"
                        className="form-input w-full rounded-lg text-[#140d1b] dark:text-white focus:outline-0 border border-gray-300 dark:border-gray-600 bg-background-light dark:bg-background-dark h-12 sm:h-14 placeholder:text-gray-500 dark:placeholder:text-gray-400 p-3 sm:p-4 pr-12 text-base font-normal leading-normal focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors"
                        required
                        minLength="6"
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400 hover:text-primary transition-colors"
                        aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                      >
                        <span className="material-symbols-outlined text-xl">
                          {showConfirmPassword ? "visibility_off" : "visibility"}
                        </span>
                      </button>
                    </div>
                  </div>

                  {/* Terms and Conditions */}
                  <div className="flex items-start gap-2 mt-2">
                    <input
                      id="terms"
                      type="checkbox"
                      className="mt-1 rounded focus:ring-primary text-primary"
                      required
                    />
                    <label htmlFor="terms" className="text-sm text-gray-600 dark:text-gray-400">
                      I agree to the{' '}
                      <a href="/terms" className="text-primary hover:underline font-medium">
                        Terms of Service
                      </a>{' '}
                      and{' '}
                      <a href="/privacy" className="text-primary hover:underline font-medium">
                        Privacy Policy
                      </a>
                    </label>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="flex items-center justify-center h-12 sm:h-14 px-6 rounded-lg w-full bg-primary text-white text-base font-semibold hover:bg-primary/90 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2 dark:focus:ring-offset-background-dark mt-4"
                  >
                    Create Account
                  </button>
                </form>

                {/* Login Link */}
                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Already have an account?{' '}
                    <Link
                      to="/login" 
                      className="font-semibold text-primary hover:underline transition-colors"
                    >
                      Log In
                    </Link>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full py-6 px-4 sm:px-6 lg:px-8 mt-auto">
        <div className="container mx-auto max-w-7xl text-center text-sm text-gray-500 dark:text-gray-400">
          <a 
            href="/terms" 
            className="hover:text-primary transition-colors"
          >
            Terms of Service
          </a>
          <span className="mx-2">·</span>
          <a 
            href="/privacy" 
            className="hover:text-primary transition-colors"
          >
            Privacy Policy
          </a>
          <span className="mx-2">·</span>
          <a 
            href="/contact" 
            className="hover:text-primary transition-colors"
          >
            Contact Us
          </a>
          <div className="mt-2 text-xs">
            © {new Date().getFullYear()} Consistency30. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default RegisterPage;