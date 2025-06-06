from rest_framework import serializers
from .models import Funcionario, Disciplina, AmbienteAula, SalaDeAula
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class FuncionarioSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Funcionario
        fields = ['id', 'NI', 'username', 'email', 'telefone', 'dt_nascimento', 'cargo', 'first_name', 'last_name', 'full_name', 'data_contratacao', 'password'] 
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        funcionario = Funcionario.objects.create_user(
            NI = validated_data['NI'],
            username = validated_data['username'],
            telefone = validated_data['telefone'],
            dt_nascimento = validated_data['dt_nascimento'],
            email = validated_data['email'],
            cargo = validated_data['cargo'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            data_contratacao = validated_data['data_contratacao'],
            password = validated_data['password'],
        )

        return funcionario
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for chave, valor in validated_data.items():
            setattr(instance, chave, valor)
        
        instance.set_password(password)

        instance.save()

        return instance

    def get_full_name(self,obj):
        return obj.get_full_name()

class SalaDeAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaDeAula
        fields = ['id', 'nome']

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id', 'nome', 'carga_horaria', 'descricao', 'professor']
        
        extra_kwargs = {
            'nome': {'required': True},
            'carga_horaria': {'required': True},
            'descricao': {'required': True},
            'professor': {'required': True}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['professor'] = f"{Funcionario.objects.get(id=representation['professor']).get_full_name()}"

        return representation

class AmbienteAulaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = AmbienteAula
        fields = ['id', 'sala_reservada', 'disciplina', 'dt_inicio', 'dt_termino', 'periodo', 'professor']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['professor'] = f"{Funcionario.objects.get(id=representation['professor']).get_full_name()}"
        representation['disciplina'] = f"{Disciplina.objects.get(id=representation['disciplina'])}"
        representation['sala_reservada'] = f"{SalaDeAula.objects.get(id=representation['sala_reservada'])}"

        return representation

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['funcionario'] = {
            'username': self.user.username,
            'cargo': self.user.cargo,
            'user_id': self.user.id
        }
        return data