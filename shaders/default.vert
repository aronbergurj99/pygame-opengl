attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_texcord0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

varying vec2 v_uv;
varying vec3 v_position;
varying vec3 v_normal;

void main(void)
{
	v_uv = a_texcord0;
	v_position = vec3(m_model * vec4(a_position, 1.0));
	v_normal = mat3(transpose(inverse(m_model))) * normalize(a_normal);
	gl_Position = m_proj * m_view * m_model * vec4(a_position, 1.0);
}