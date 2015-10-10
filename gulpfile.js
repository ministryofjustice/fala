/* jshint node: true */

var gulp = require('gulp');
var gutil = require("gulp-util");
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var webpack = require('webpack');
try {
  var browserSync = require('browser-sync').create();
} catch(e) {}

var importPaths = require('mojular-govuk-elements').getPaths('sass').concat(require('mojular-moj-elements').getPaths('sass'));

var paths = {
  src: 'fala/assets-src/',
  dest: 'fala/assets/',
  styles: 'fala/assets-src/sass/**/*.scss',
  scripts: 'fala/assets-src/scripts/**/*.js',
  images: 'node_modules/mojular-govuk-elements/assets/images/*'
};

gulp.task('sass', function() {
  var result = gulp.src(paths.styles)
    .pipe(sourcemaps.init())
    .pipe(sass({ includePaths: importPaths }).on('error', sass.logError))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.dest + 'css/'))

    try {
      result.pipe(browserSync.stream({match: '**/*.css'}));
    } catch(e) {}
  return result;
});

gulp.task('scripts', function(callback) {
  webpack(require('./webpack.config.js')).run(function(err, stats) {
    if(err) throw new gutil.PluginError("webpack", err);
    gutil.log("[webpack]", stats.toString({
      colors: true,
      modules: false,
      chunkModules: false
    }));
    callback();
  });
});

gulp.task('images', function() {
  return gulp.src(paths.images)
    .pipe(gulp.dest(paths.dest + 'images/'));
});

gulp.task('serve', ['build'], function() {
  browserSync.init({
    proxy: 'localhost:8000',
    open: false,
    port: 3000
  });

  gulp.watch(paths.images, ['images']);
  gulp.watch(paths.styles, ['sass']);
  gulp.watch([
    'node_modules/mojular-govuk-elements/**/*.scss',
    'node_modules/mojular-moj-elements/**/*.scss'
  ], ['sass']);
  gulp.watch(paths.scripts, ['scripts']).on('change', browserSync.reload);
});

gulp.task('build', ['sass', 'images', 'scripts']);

gulp.task('default', ['build']);
