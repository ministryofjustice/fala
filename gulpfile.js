/* jshint node: true */

'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var readJson = require('read-json-sync');
var concat = require('gulp-concat');
var util = require('util');
var merge = require('merge-stream');

var bowerDir = 'bower_components';

try {
  bowerDir = readJson('.bowerrc').directory;
} catch(e) {}

var paths = {
  src: __dirname + '/fala/assets-src/',
  dest: __dirname + '/fala/assets/',
  styles: __dirname + '/fala/assets-src/sass/**/*.scss',
  js: __dirname + '/fala/assets-src/js/**/*.js',
  mojular_js: [
    util.format('%s/mojular/assets/scripts/moj.js', bowerDir),
    util.format('%s/mojular/assets/scripts/modules/**/*.js', bowerDir),
    util.format('%s/mojular/assets/scripts/moj-init.js', bowerDir)
  ]
};

gulp.task('sass', function() {
  var importPaths = [];

  importPaths = importPaths.concat(readJson(util.format('%s/govuk-template/paths.json', bowerDir)).import_paths);
  importPaths = importPaths.concat(readJson(util.format('%s/mojular/paths.json', bowerDir)).import_paths);

  gulp.src(paths.styles)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: importPaths.map(function(path) {
        return util.format('%s/%s', bowerDir, path);
      })
    }).on('error', sass.logError))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.dest + 'css/'));
});

gulp.task('js', function() {
  var local_js = gulp.src(paths.mojular_js).pipe(concat('moj.js')).pipe(gulp.dest(paths.dest + 'scripts/'));
  var mojular_js = gulp.src(paths.js).pipe(concat('application.js')).pipe(gulp.dest(paths.dest + 'scripts/'));

  return merge(local_js, mojular_js);
});

gulp.task('default', ['js', 'sass']);
