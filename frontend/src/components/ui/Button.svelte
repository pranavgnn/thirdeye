<script lang="ts">
  import { cn } from "@/lib/utils";

  type Variant =
    | "default"
    | "destructive"
    | "outline"
    | "secondary"
    | "ghost"
    | "link";
  type Size = "default" | "sm" | "lg" | "icon";

  let className: string | undefined = undefined;
  export { className as class };
  export let variant: Variant = "default";
  export let size: Size = "default";
  export let disabled: boolean = false;
  export let type: "button" | "submit" | "reset" = "button";

  const variants = {
    default: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-md hover:shadow-lg active:scale-95",
    destructive:
      "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-md hover:shadow-lg active:scale-95",
    outline:
      "border-2 border-primary bg-background hover:bg-primary hover:text-primary-foreground shadow-sm hover:shadow-md active:scale-95",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 shadow-sm hover:shadow-md active:scale-95",
    ghost: "hover:bg-accent hover:text-accent-foreground active:scale-95",
    link: "text-primary underline-offset-4 hover:underline",
  };

  const sizes = {
    default: "h-11 px-6 py-2 text-base",
    sm: "h-9 px-4 text-sm",
    lg: "h-13 px-8 text-lg",
    icon: "h-11 w-11",
  };
</script>

<button
  {type}
  {disabled}
  class={cn(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
    variants[variant],
    sizes[size],
    className
  )}
  on:click
>
  <slot />
</button>
