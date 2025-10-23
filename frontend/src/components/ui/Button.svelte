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
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
    destructive:
      "bg-destructive text-destructive-foreground hover:bg-destructive/90",
    outline:
      "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
    secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
    ghost: "hover:bg-accent hover:text-accent-foreground",
    link: "text-primary underline-offset-4 hover:underline",
  };

  const sizes = {
    default: "h-10 px-4 py-2",
    sm: "h-9 rounded-lg px-3 text-xs",
    lg: "h-11 rounded-lg px-8",
    icon: "h-10 w-10",
  };
</script>

<button
  {type}
  {disabled}
  class={cn(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
    variants[variant],
    sizes[size],
    className
  )}
  on:click
>
  <slot />
</button>
