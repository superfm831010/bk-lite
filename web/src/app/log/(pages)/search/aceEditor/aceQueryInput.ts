// 自定义查询输入主题
/* eslint-disable @typescript-eslint/no-explicit-any */
import ace from 'ace-builds/src-noconflict/ace';

ace.define(
  'ace/theme/ace-queryinput',
  ['require', 'exports', 'module', 'ace/lib/dom'],
  (acequire: any, exports: any) => {
    exports.isDark = false;
    exports.cssClass = 'ace-queryinput';

    const dom = acequire('../lib/dom');

    exports.cssText = `
.ace-queryinput {
  border: 1px solid var(--color-border-3);
  border-radius: 4px 0 0 4px;
  background: var(--color-bg-2);
  min-height: 32px;
}

.ace-queryinput .ace_content {
  top: 8px !important;
  right: 40px !important;
}

.ace-queryinput .ace_cursor {
  color: var(--color-text-2) !important;
  top: 1px !important;
}

.ace-queryinput .ace_text-layer {
  margin-top: 4px;
}

.ace_editor.ace_autocomplete {
  width: 600px !important;
  margin-top: 8px;
  background: var(--color-bg-2);
  color: var(--color-text-1);
}

.ace_multiselect .ace_selection.ace_start {
    box-shadow: 0 0 3px 0 var(--color-bg-2);
}

.ace_gutter {
    background: var(--color-bg-2);
    color: var(--color-text-2);
}

.ace_print-margin {
    width: 1px;
    background: var(--color-bg-2);
}

.ace_cursor {
    color: var(--color-text-2);
    display: block;
}

.ace_hidden-cursors {
    display: none;
}

.ace_marker-layer .ace_selection {
    background: var(--color-fill-2);
}

.ace_marker-layer .ace_step {
    background: #faad14;
}

.ace_marker-layer .ace_bracket {
    margin: -1px 0 0 -1px;
    border: none;
}

.ace_marker-layer .ace_active-line {
    background: var(--color-bg-2);
}

.ace_gutter-active-line {
    background: var(--color-bg-2);
}

.ace_marker-layer .ace_selected-word {
    border: 1px solid var(--color-border-2);
}

.ace_invisible {
    color: var(--color-bg-2);
}

.ace_keyword,
.ace_meta,
.ace_storage,
.ace_storage.ace_type,
.ace_support.ace_type {
    color: var(--color-primary);
}

.ace_keyword.ace_operator {
    color: var(--color-primary);
}

.ace_constant.ace_character,
.ace_constant.ace_language,
.ace_constant.ace_numeric,
.ace_keyword.ace_other.ace_unit,
.ace_support.ace_constant,
.ace_variable.ace_parameter {
    color: var(--color-fail);
}

.ace_constant.ace_other {
    color: var(--color-text-1);
}

.ace_invalid {
    color: var(--color-text-1);
    background-color: var(--color-bg-2);
}

.ace_invalid.ace_deprecated {
    color: var(--color-primary);
    background-color: var(--color-fill-2);
}

.ace_fold {
    background-color: var(--color-primary);
    border-color: var(--color-text-4);
}

.ace_entity.ace_name.ace_function,
.ace_support.ace_function,
.ace_variable,
.ace_term {
    color: var(--color-primary);
}

.ace_completion-highlight {
    color: var(--color-primary) !important;
}

.ace_support.ace_class,
.ace_support.ace_type {
    color: #faad14;
}

.ace_heading,
.ace_markup.ace_heading,
.ace_string {
    color: var(--color-success);
}

.ace_entity.ace_name.ace_tag,
.ace_entity.ace_other.ace_attribute-name,
.ace_meta.ace_tag,
.ace_string.ace_regexp,
.ace_variable {
    color: var(--color-primary);
}

.ace_comment {
    color: var(--color-text-4);
}

.ace_indent-guide {
    background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAE0lEQVQImWP4////f4bdu3f/BwAlfgctduB85QAAAABJRU5ErkJggg==) right repeat-y;
}

.ace-placeholder {
    position: absolute;
    left: 6px;
    top: 8px;
    font-size: 12px;
    color: var(--color-text-4);
    cursor: text;
}

.ace_marker {
    border-bottom: 2px dashed;
    position: absolute;
    border-radius: 0;
    margin-top: 1px;
}

.ace_marker.ace_validation_error {
    border-color: var(--color-fail);
}

.ace_marker.ace_validation_warning {
    border-color: #faad14;
}

.ace_autocomplete > .ace_scroller > .ace_content {
    top: -2px !important;
}

.ace_rightAlignedText {
    color: var(--color-text-3);
}

.ace_scrollbar-h {
    display: none;
}

.ace_scroller.ace_scroll-left {
    box-shadow: none !important;
}
`;

    dom.importCssString(exports.cssText, exports.cssClass);
  }
);

export {};
