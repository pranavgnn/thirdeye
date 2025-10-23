<script lang="ts">
  import { cn } from "@/lib/utils";

  let className: string | undefined = undefined;
  export { className as class };
</script>

<div
  class={cn("relative w-full rounded-lg border px-4 py-3 text-sm", className)}
  role="alert"
>
  <slot />
</div>
