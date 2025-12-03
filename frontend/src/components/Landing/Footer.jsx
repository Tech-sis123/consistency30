import React from 'react';

const Footer = () => {
  return (
    <footer className="border-t border-header-border-dark mt-10 py-8">
      <div className="flex flex-col md:flex-row justify-between items-center gap-6 px-4">
        <div className="flex items-center gap-2">
          <div className="size-5 text-primary">
            <span className="material-symbols-outlined !text-3xl">
              all_inclusive
            </span>
          </div>
          <p className="text-text-muted-dark text-sm">
            © 2024 Consistency30. All rights reserved.
          </p>
        </div>
        
        <div className="flex gap-6 items-center">
          <a className="text-text-muted-dark text-sm hover:text-white transition-colors" href="#">
            Terms of Service
          </a>
          <a className="text-text-muted-dark text-sm hover:text-white transition-colors" href="#">
            Privacy Policy
          </a>
        </div>
        
        <div className="flex gap-4">
          <a className="text-text-muted-dark hover:text-white transition-colors" href="#">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"></path>
            </svg>
          </a>
          <a className="text-text-muted-dark hover:text-white transition-colors" href="#">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.85s-.012 3.584-.07 4.85c-.148 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07s-3.584-.012-4.85-.07c-3.252-.148-4.771-1.691-4.919-4.919-.058-1.265-.069-1.645-.069-4.85s.012-3.584.07-4.85C2.165 3.854 3.709 2.31 6.96 2.163 8.216 2.105 8.596 2.093 12 2.093zm0 1.625c-3.174 0-3.542.01-4.78.068-2.7.123-3.996 1.424-4.12 4.12C3.04 9.17 3.03 9.54 3.03 12.7s.01 3.53.068 4.78c.124 2.695 1.42 3.996 4.12 4.12 1.238.058 1.606.068 4.78.068s3.542-.01 4.78-.068c2.7-.124 3.996-1.425 4.12-4.12.058-1.25.068-1.62.068-4.78s-.01-3.53-.068-4.78C20.956 5.218 19.66 3.917 16.96 3.793c-1.238-.057-1.606-.067-4.78-.067zm0 3.375c-2.43 0-4.39 1.96-4.39 4.39s1.96 4.39 4.39 4.39 4.39-1.96 4.39-4.39-1.96-4.39-4.39-4.39zm0 7.163c-1.528 0-2.773-1.245-2.773-2.773S10.472 9.227 12 9.227s2.773 1.245 2.773 2.773-1.245 2.773-2.773 2.773zm4.92-7.23a1.03 1.03 0 100-2.06 1.03 1.03 0 000 2.06z"></path>
            </svg>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;