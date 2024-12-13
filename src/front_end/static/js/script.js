


function switchInfoDisplay(btn) {
    const courseInfo = btn.querySelector('.course-info');
    const homeworksInfo = btn.querySelector('.homeworks-info');

    courseInfo.classList.toggle('info-display-func');
    homeworksInfo.classList.toggle('info-display-func');
    btn.classList.toggle('btn-scale-func')
}