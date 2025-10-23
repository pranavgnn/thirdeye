<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
    onclick?: (e: MouseEvent) => void;
  }

  let { children, class: className = "", onclick }: Props = $props();
</script>

<tr
  class="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted {className}"
  {onclick}
  role={onclick ? "button" : undefined}
  tabindex={onclick ? 0 : undefined}
>
  {#if children}
    {@render children()}
  {/if}
</tr>
