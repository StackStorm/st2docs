$( document ).ready(function() {
    // Open external links in another tab/window
    $(".external").attr("target","_blank");
    // List the docs version in breadcrumbs
    $(".wy-breadcrumbs li a.icon-home").text(
        "Docs "
        // TODO: get the version, not just the slug
        // + "v"
        + $(".wy-side-nav-search>div.version").text()
    )
});
