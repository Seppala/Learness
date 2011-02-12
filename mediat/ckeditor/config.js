/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/



CKEDITOR.editorConfig = function( config )
{
    config.toolbar = 'MyToolbar';
 
    config.toolbar_MyToolbar =
    [
        ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Scayt'],
        ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
        ['Image','Flash','Table','HorizontalRule','SpecialChar'],
        '/',
        ['Bold','Italic','Strike','Subscript','Superscript'],
        ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
        ['Link','Unlink','Anchor'],
        ['Styles','Format','Font','FontSize'],
        ['TextColor','BGColor']
        ['Maximize','-']
    ];
};
