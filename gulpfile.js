const gulp = require('gulp');
const sourcemaps = require('gulp-sourcemaps');
const concat = require('gulp-concat');
const terser = require('gulp-terser');
const cleanCss = require('gulp-clean-css');
const sass = require('gulp-sass')(require('sass'));
const { src, parallel, dest} = require('gulp'); 

// FALA js & GOVUK js - copying over both if we ever want to add custom js
const jsPath = [
  'fala/assets-src/scripts/cookies.js',
  'node_modules/govuk-frontend/dist/govuk/govuk-frontend.min.js'
];

// FALA css & GOVUK css - because we import GOVUK scss into same file in order to override/add to GOVUK classes
const cssPath = 'fala/assets-src/sass/*.scss';

// GOVUK font & images only - because we have no FALA assets any more
const assetPath = 'node_modules/govuk-frontend/dist/govuk/assets/**';


 function jsTask() {
  return src(jsPath)
  .pipe(sourcemaps.init())
  // name of output file
  .pipe(concat('all.js'))
  // a JavaScript mangler/compressor toolkit for ES6+
  .pipe(terser())
  .pipe(sourcemaps.write('.'))
  // destination of new files
  .pipe(dest('fala/assets/js'));
}

function cssTask() {
  return src(cssPath)
  .pipe(sourcemaps.init())
  .pipe(sass())
  // name of output file
  .pipe(concat('style.css'))
  // this minifies the CSS
  .pipe(cleanCss())
  .pipe(sourcemaps.write('.'))
  // destination of new files
  .pipe(dest('fala/assets/css'));
}

function assetTask() {
  // { encoding: false } to copy over as binary files, GULP default is to encode into UTF:8 
  return src(assetPath, { encoding: false })
  .pipe(dest('fala/assets'));
}

exports.jsTask = jsTask;
exports.cssTask = cssTask;
exports.assetTask = assetTask;

// build/execute the tasks
exports.build = parallel(jsTask, cssTask, assetTask);
