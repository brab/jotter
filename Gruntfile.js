/* globals require:false */
'use strict()';

module.exports = function (grunt) {
  // load all grunt tasks
  require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

  // configurable paths
  var yeomanConfig = {
    app: 'app',
    dist: 'dist',
    tmp: '.tmp'
  };

  try {
    yeomanConfig.app = require('./component.json').appPath || yeomanConfig.app;
  } catch (e) {}

  grunt.initConfig({
    yeoman: yeomanConfig,
    watch: {
      compass: {
        files: ['<%= yeoman.app %>/styles/{,*/}*.{scss,sass}'],
        tasks: ['compass:server']
      },
      less: {
        files: ['<%= yeoman.app %>/styles/*.less'],
        tasks: ['less:server']
      },
      html2js: {
        files: ['<%= yeoman.app %>/templates/**/*.html'],
        tasks: ['htmlmin', 'html2js']
      },
      karma: {
        files: [
          '<%= yeoman.app %>/scripts/**/*.js',
          '<%= yeoman.app %>/views/**/*.html',
          'test/spec/**/*.js'
        ],
        tasks: ['karma:unit']
      }
    },
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= yeoman.dist %>/*',
            '!<%= yeoman.dist %>/.git*'
          ]
        }]
      },
      server: '<%= yeoman.tmp %>'
    },
    jshint: {
      options: {
        jshintrc: '.jshintrc'
      },
      all: [
        'Gruntfile.js',
        '<%= yeoman.app %>/scripts/{,*/}*.js'
      ]
    },
    karma: {
      build: {
        autowatch: false,
        background: false,
        configFile: 'karma.conf.js',
        singleRun: true,
      },
      unit: {
        autowatch: false,
        background: true,
        configFile: 'karma.conf.js',
        singleRun: false,
      }
    },
    compass: {
      options: {
        sassDir: '<%= yeoman.app %>/styles',
        cssDir: '<%= yeoman.app %>/styles',
        imagesDir: '<%= yeoman.app %>/images',
        javascriptsDir: '<%= yeoman.app %>/scripts',
        fontsDir: '<%= yeoman.app %>/styles/fonts',
        importPath: '<%= yeoman.app %>/components',
        relativeAssets: true
      },
      dist: {},
      server: {
        options: {
          debugInfo: true
        }
      }
    },
    less: {
      options: {
        compile: true
      },
      dist: {
        options: {
          compress: true
        },
        src: ['<%= yeoman.app %>/styles/bootstrap-jotter.less'],
        dest: '<%= yeoman.dist %>/styles/bootstrap-jotter.css'
      },
      server: {
        src: ['<%= yeoman.app %>/styles/bootstrap-jotter.less'],
        dest: '<%= yeoman.app %>/styles/bootstrap-jotter.css'
      }
    },
    concat: {
      dist: {
        files: {
          '<%= yeoman.tmp %>/scripts/scripts.js': [
            '<%= yeoman.app %>/scripts/app.js',
            '<%= yeoman.app %>/scripts/templates.js',
            '<%= yeoman.app %>/scripts/controllers/*.js',
            '<%= yeoman.app %>/scripts/directives/*.js',
            '<%= yeoman.app %>/scripts/services/*.js',
          ]
        }
      }
    },
    useminPrepare: {
      html: '<%= yeoman.app %>/index.html',
      options: {
        dest: '<%= yeoman.dist %>'
      }
    },
    usemin: {
      html: ['<%= yeoman.dist %>/**/*.html'],
      css: ['<%= yeoman.dist %>/styles/*.css'],
      options: {
        dirs: ['<%= yeoman.dist %>']
      }
    },
    imagemin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '{,*/}*.{png,jpg,jpeg}',
          dest: '<%= yeoman.dist %>/images'
        }]
      }
    },
    cssmin: {
      dist: {
        files: {
          '<%= yeoman.dist %>/styles/main.css': [
            '<%= yeoman.app %>/styles/main.css'
          ],
          '<%= yeoman.dist %>/styles/bootstrap-jotter.css': [
            '<%= yeoman.app %>/styles/bootstrap-jotter.css'
          ]
        }
      }
    },
    htmlmin: {
      dist: {
        options: {
          // https://github.com/yeoman/grunt-usemin/issues/44
          collapseWhitespace: true,
        },
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>',
          src: [
            '*.html',
            'templates/**/*.html',
            '!index.html'
          ],
          dest: '<%= yeoman.tmp %>'
        }]
      }
    },
    html2js: {
      options: {
        module: 'jotterTemplates',
        base: '<%= yeoman.tmp %>'
      },
      '<%= yeoman.app %>/scripts/templates.js': [ '<%= yeoman.tmp %>/templates/**/*.html' ]
    },
    ngmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.dist %>/scripts',
          src: '*.js',
          dest: '<%= yeoman.dist %>/scripts'
        }]
      }
    },
    uglify: {
      dist: {
        files: {
          '<%= yeoman.dist %>/scripts/scripts.js': [
            '<%=yeoman.tmp %>/scripts/scripts.js'
          ]
        }
      }
    },
    rev: {
      dist: {
        files: {
          src: [
            '<%= yeoman.dist %>/scripts/**/*.js',
            '<%= yeoman.dist %>/styles/*.css',
            '<%= yeoman.dist %>/styles/fonts/*',
            '<%= yeoman.dist %>/images/**/*.{png,jpg,jpeg,gif,webp}'
          ]
        }
      }
    },
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= yeoman.app %>',
          dest: '<%= yeoman.dist %>',
          src: [
            '*.{ico,txt,html}',
            'components/**/*',
            'images/{,*/}*.{png,jpg,gif,webp}',
            'views/**/*',
            'components/**/*.{js,css,png,gif,jpg}',
            '!components/**/test?/**/*',
            '!components/**/docs/**/*',
            '!components/**/*.html',
            '!components/bootstrap/*.css'
          ]
        }]
      }
    },
    shell: {
      options: {
        stdout: true,
        stderr: true,
        failOnErr: true
      },
      runserver: {
        command: function () {
          return './manage.py runserver 192.168.33.10:8000';
        },
        options: {
          execOptions: {
            cwd: 'server'
          },
        }
      }
    },
    parallel: {
      run: {
        options: {
          force: true,
          grunt: true,
          stream: true
        },
        tasks: [
          'simple-watch',
          'shell:runserver'
        ]
      }
    }
  });

  grunt.renameTask('regarde', 'watch');

  grunt.registerTask('server', [
    'clean:server',
    'compass:server',
    'watch'
  ]);

  grunt.registerTask('test', [
    'clean:server',
    'compass',
    'less',
    'karma:build'
  ]);

  grunt.registerTask('build', [
    'clean:dist',
    'test',
    'compass:dist',
    'less:dist',
    'htmlmin:dist',
    'html2js',
    'useminPrepare',
    'concat',
    'imagemin',
    'cssmin',
    'copy:dist',
    'ngmin',
    'uglify:dist',
    'rev',
    'usemin'
  ]);

  grunt.registerTask('default', ['parallel:run']);
};
