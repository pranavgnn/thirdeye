<script lang="ts">
  import { onMount } from "svelte";
  import Home from "@/routes/Home.svelte";
  import Privacy from "@/routes/Privacy.svelte";
  import Reports from "@/routes/Reports.svelte";
  import Upload from "@/routes/Upload.svelte";
  import Admin from "@/routes/Admin.svelte";
  import NotFound from "@/routes/NotFound.svelte";
  import ThemeToggle from "@/components/ThemeToggle.svelte";

  let currentPath = $state(window.location.pathname);

  function navigate(event: MouseEvent) {
    const target = event.target as HTMLElement;
    const anchor = target.closest("a");
    if (
      anchor &&
      anchor.href &&
      anchor.origin === window.location.origin &&
      !anchor.hasAttribute("download") &&
      !anchor.target
    ) {
      event.preventDefault();
      const path = new URL(anchor.href).pathname;
      window.history.pushState({}, "", path);
      currentPath = path;
    }
  }

  function handlePopState() {
    currentPath = window.location.pathname;
  }

  onMount(() => {
    currentPath = window.location.pathname;
  });
</script>

<svelte:window onclick={navigate} onpopstate={handlePopState} />

<ThemeToggle />

{#if currentPath === "/"}
  <Home />
{:else if currentPath === "/privacy"}
  <Privacy />
{:else if currentPath === "/reports"}
  <Reports />
{:else if currentPath === "/upload"}
  <Upload />
{:else if currentPath === "/admin"}
  <Admin />
{:else}
  <NotFound />
{/if}
