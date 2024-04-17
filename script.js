// Get the body element
const insert_here = document.getElementById('insert_here');

// Set the initial slide index
let slideIndex = 0;
let slideLength = 1;
// Function to update the slide
function updateSlide() {
    // Clear the body content
    insert_here.innerHTML = '';
    fetch('./slides.json')
    .then(response => response.json()).then(data => data.slides)
    .then(slides => {
        const slide = slides[slideIndex % slides.length];
        slideLength = slides.length;

        if (slide.type === 'text') {
            const p = document.createElement('p');
            let fontmultiplier = 1;
            if (slide.content.length == 1) {
                insert_here.style.textAlign = 'center';
            } else {
                insert_here.style.textAlign = 'left';
                fontmultiplier = .8;
            }
            p.textContent = slide.content.join('\n');
            p.style.fontSize = `calc(6.4vw * ${fontmultiplier})`;
            // if (slide.bulletPoints) {
            //     const ul = document.createElement('ul');
            //     slide.bulletPoints.forEach(bulletPoint => {
            //         const li = document.createElement('li');
            //         li.textContent = bulletPoint;
            //         ul.appendChild(li);
            //     });
            //     p.appendChild(ul);
            // }


            insert_here.appendChild(p);
        } else if (slide.type === 'image') {
            const img = document.createElement('img');
            img.src = slide.url;
            img.className = 'centered';
            img.style.height = '800px';
            insert_here.appendChild(img);
        }
    });
}

function invertColors() {
    if (document.body.style.backgroundColor === 'black') {
        document.body.style.backgroundColor = 'white';
        document.body.style.color = 'black';
        return;
    }
    document.body.style.backgroundColor = 'black';
    document.body.style.color = 'white';

}

// Function to handle key events
function handleKeyEvents(event) {
    if (event.key === 'ArrowLeft') {
        // Decrease the slide index
        if (slideIndex !== 0) {
            slideIndex--
            updateSlide();
        }
    } else if (event.key === 'ArrowRight') {
        // Increase the slide index
        if (slideIndex !== slideLength - 1) {
            slideIndex++;
            updateSlide();
        }
    } else if (event.key === 'i') {
        invertColors();
    }
}

// Add event listener for keydown events
document.addEventListener('keydown', handleKeyEvents);

// Initial update of the slide
updateSlide();