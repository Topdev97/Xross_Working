const accordionHeader = document.querySelectorAll(".accordion-header");
accordionHeader.forEach((header) => {
    header.addEventListener("click", function() {

        const accordionContent = header.parentElement.querySelector(".accordion-content");
        
        // Condition handling
        if (header.querySelector(".fas").classList.contains("fa-chevron-down")) {
            accordionContent.style.maxHeight = `${accordionContent.scrollHeight + 32}px`;
            header.querySelector(".fas").classList.remove("fa-chevron-down");
            header.querySelector(".fas").classList.add("fa-chevron-up");
        } else {
            accordionContent.style.maxHeight = "0px";
            header.querySelector(".fas").classList.add("fa-chevron-down");
            header.querySelector(".fas").classList.remove("fa-chevron-up");
        }
    });
});