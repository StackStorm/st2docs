$( document ).ready(function() {
    // Open external links in another tab/window
    $(".external").attr("target","_blank");
    // List the docs version in breadcrumbs
    $(".wy-breadcrumbs li a.icon-home").text(
        // DOCUMENTATION_OPTIONS is a sphinx feature
        "Docs v" + DOCUMENTATION_OPTIONS.VERSION
    )
});
