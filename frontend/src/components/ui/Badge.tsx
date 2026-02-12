import { HTMLAttributes } from "react";
import { clsx } from "clsx";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "primary" | "secondary" | "outline";
}

export default function Badge({
  className,
  variant = "default",
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        {
          "bg-stone-100 text-stone-800": variant === "default",
          "bg-amber-100 text-amber-900": variant === "primary",
          "bg-green-100 text-green-800": variant === "secondary",
          "border border-stone-300 text-stone-700": variant === "outline",
        },
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
