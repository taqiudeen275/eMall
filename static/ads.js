// static/js/popup_ad.js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showPopupAd() {
    fetch('/get-popup-ad/')
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                const adHtml = `
                    <div id="popup-ad" class="popup-ad">
                        <div class="popup-ad-content ">
                            <span class="close-ad">&times;</span>
                            <div class="flex">
                            <img src="${data.image_url}" class="ads-img col" alt="${data.title}">
                            <div class="info">
                            <h2>${data.title}</h2>
                            <p>${data.description}</p>
                            <a href="${data.url}" class="ad-link col" data-ad-id="${data.id}">Learn More</a>
                            </div>
                            </div>
                        </div>
                    </div>
                `;
                document.body.insertAdjacentHTML('beforeend', adHtml);
                
                document.querySelector('.close-ad').addEventListener('click', () => {
                    document.getElementById('popup-ad').style.display = 'none';
                });
                
                document.querySelector('.ad-link').addEventListener('click', (e) => {
                    e.preventDefault();
                    const adId = e.target.getAttribute('data-ad-id');
                    fetch(`/record-ad-click/${adId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    }).then(() => {
                        window.location.href = e.target.href;
                    });
                });
            }
        });
}

// Show the pop-up ad after a 5-second delay
setTimeout(showPopupAd, 5000);