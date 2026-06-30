import * as React from "react";

import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost";
};

export function Button({ className, variant = "primary", ...props }: ButtonProps) {
  const variants = {
    primary: "bg-primary text-white hover:opacity-90",
    secondary: "border border-border bg-card text-foreground hover:bg-white/5",
    ghost: "text-muted hover:text-foreground"
  };
  return (
    <button
      className={cn(
        "inline-flex min-h-10 items-center justify-center rounded-lg px-4 text-sm font-bold transition",
        variants[variant],
        className
      )}
      {...props}
    />
  );
}

