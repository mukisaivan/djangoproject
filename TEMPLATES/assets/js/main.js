// hero section img changer
const heroSection = document.querySelector('.hero');
const heroSideImgs = document.querySelectorAll('.side-imgs img');
const imgLocation = document.querySelector('.img-location');

let currentImgIndex = 0;

// const increaseImgIndex = () => currentImgIndex = currentImgIndex + 1;

const changeInterval = setInterval(() => {
    currentImgIndex = currentImgIndex + 1;
}, 5000);

heroSideImgs.forEach(img => {
    img.addEventListener('click', () => changeHeroBackground(img))
});

const changeHeroBackground = (img) => {
    const imgId = parseInt(img.dataset.index);
    currentImgIndex = imgId;
    imgLocation.querySelector('span').textContent = img.dataset.location;
    setHeroBackground();
}

// const autoImgChange = () => {
//     setInterval(() => {
//         if (currentImgIndex < heroSideImgs.length)
//         {
//             currentImgIndex++;
//         }
//         else
//         {
//             currentImgIndex = 0;
//         }
//         console.log(currentImgIndex)
//         setHeroBackground();
//     }, 5000);
// }

const setHeroBackground = () => {
    const imgUrl = heroSideImgs[currentImgIndex].src;
    heroSection.style.backgroundImage = `url(${imgUrl})`;

    imgLocation.querySelector('span').textContent = heroSideImgs[currentImgIndex].dataset.location;
    // autoImgChange();
}

setHeroBackground();