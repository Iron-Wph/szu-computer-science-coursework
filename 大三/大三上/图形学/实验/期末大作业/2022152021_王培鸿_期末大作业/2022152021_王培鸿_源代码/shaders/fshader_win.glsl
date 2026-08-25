#version 330 core

// 给光源数据一个结构体
struct Light{
	vec4 ambient;
	vec4 diffuse;
	vec4 specular;
	vec3 position;
    // 光源衰减系数的三个参数
    float constant; // 常数项
    float linear;	// 一次项
    float quadratic;// 二次项

};

// 给物体材质数据一个结构体
struct Material{
	vec4 ambient;
	vec4 diffuse;
	vec4 specular;

	float shininess;
};

in vec3 position;
in vec3 normal;
in vec2 texCoord;

// 相机坐标
uniform vec3 eye_position;
// 光源
uniform Light light;
// 物体材质
uniform Material material;
uniform int isShadow;
// 纹理数据
uniform sampler2D texture;

out vec4 fColor;

void main()
{
	if (isShadow == 1) {
		fColor = vec4(0.0, 0.0, 0.0, 1.0);
	}
	else {
		vec4 texColor = texture2D( texture, texCoord );
    	// 环境光分量I_a
    	vec4 I_a = light.ambient * material.ambient;
		// 漫反射分量I_d
    	vec3 L = normalize(light.position - position);
    	vec3 N = normalize(normal);
    	float diffuse_dot = max(dot(N, L), 0.0);
    	vec4 I_d = diffuse_dot * light.diffuse * material.diffuse;
    	// 镜面反射分量I_s
    	vec3 V = normalize(eye_position - position);
    	vec3 R = normalize(-reflect(L, N));
    	float specular_dot = pow(max(dot(R, V), 0.0), material.shininess);
    	vec4 I_s = specular_dot * light.specular * material.specular;
		// 注意如果光源在背面则去除高光
		if( dot(L, N) < 0.0 ) {
		    I_s = vec4(0.0, 0.0, 0.0, 1.0);
		}
    	// 累加所有光照分量
    	fColor = (I_a + I_d + I_s) * texColor;
		fColor.a = 1.0;
	}
}
