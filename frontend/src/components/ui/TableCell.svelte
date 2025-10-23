<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    class?: string;
  }

  let { children, class: className = "" }: Props = $props();
</script>

<td class="p-4 align-middle [&:has([role=checkbox])]:pr-0 {className}">
  {#if children}
    {@render children()}
  {/if}
</td>
