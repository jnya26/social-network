from alembic import op
import sqlalchemy as sa

revision = 'bcb5947d9990'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('username', sa.String(), nullable=True),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('activities',
                    sa.Column('action', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('autor_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['autor_id'], ['user.id'], name='fk_post_autor_id', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('followers',
                    sa.Column('follower_id', sa.Integer(), nullable=False),
                    sa.Column('followee_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['followee_id'], ['user.id'], name='fk_follows_followee_id'),
                    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='fk_follows_follower_id'),
                    sa.PrimaryKeyConstraint('follower_id', 'followee_id')
                    )
    op.create_table('posts',
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('autor_id', sa.Integer(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['autor_id'], ['user.id'], name='fk_post_autor_id', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('profiles',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=True),
                    sa.Column('last_name', sa.String(), nullable=True),
                    sa.Column('bio', sa.String(), nullable=True),
                    sa.Column('last_seen', sa.DateTime(), nullable=True),
                    sa.Column('linkidln_link', sa.String(), nullable=True),
                    sa.Column('facebook_link', sa.String(), nullable=True),
                    sa.Column('country', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_profiles_user_id', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.create_index('idx_profiles_user_id', ['user_id'], unique=False)

    op.create_table('dislikes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_dislikes_post_id'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_dislikes_user_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('likes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name='fk_likes_post_id'),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_likes_user_id'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    op.drop_table('dislikes')
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_index('idx_profiles_user_id')

    op.drop_table('profiles')
    op.drop_table('posts')
    op.drop_table('followers')
    op.drop_table('activities')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
