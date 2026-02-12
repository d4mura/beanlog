import { ButtonHTMLAttributes, forwardRef } from "react";
import { clsx } from "clsx";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
          {
            "bg-amber-900 text-white hover:bg-amber-800 focus:ring-amber-900":
              variant === "primary",
            "bg-amber-100 text-amber-900 hover:bg-amber-200 focus:ring-amber-500":
              variant === "secondary",
            "border border-amber-300 text-amber-900 hover:bg-amber-50 focus:ring-amber-500":
              variant === "outline",
            "text-amber-900 hover:bg-amber-50 focus:ring-amber-500":
              variant === "ghost",
            "bg-red-600 text-white hover:bg-red-700 focus:ring-red-600":
              variant === "danger",
          },
          {
            "px-3 py-1.5 text-sm": size === "sm",
            "px-4 py-2 text-sm": size === "md",
            "px-6 py-3 text-base": size === "lg",
          },
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
export default Button;
