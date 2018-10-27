"""empty message

Revision ID: 80b647f2fe93
Revises:
Create Date: 2018-09-10 23:29:20.042229

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '80b647f2fe93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classifier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('training_samples', sa.Integer(), nullable=False),
    sa.Column('test_samples', sa.Integer(), nullable=False),
    sa.Column('accuracy', sa.Float(), nullable=False),
    sa.Column('model_hash', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spam_label',
    sa.Column('label', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('label')
    )
    op.create_table('training_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=500), nullable=True),
    sa.Column('label', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['label'], ['spam_label.label'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
    data_upgrades()


def data_upgrades():
    spam_label = table('spam_label',
                       column('label', sa.String),
                       column('created_at', sa.DateTime))
    op.bulk_insert(spam_label, [
        {'label': 'SPAM', 'created_at': datetime.utcnow()},
        {'label': 'NON-SPAM', 'created_at': datetime.utcnow()}
    ])
    training_data = table('training_data',
                          column('text', sa.String),
                          column('label', sa.String),
                          column('created_at', sa.DateTime))
    op.bulk_insert(training_data, [
        {
            'text': 'RT @ElixiumCapital: Trade with #Bitcoin',
            'label': 'SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'RT @ElixiumCapital: Trade with',
            'label': 'SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'RT @BIGMONEYMIKE6: WHEN MY NAME ( #BMM ) COMES UP , RESPEK IT !!!!',
            'label': 'SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'RT @BIGMONEYMIKE6: THINGS OF UTMOST IMPORTANCE 1) GOD 2) FAMILY 3) SELF 4) #PENNYSTOCKS 5) WIFEY',
            'label': 'SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'RT @BColwell_Invest: #Nvidia DCF Implied Valuation - $nvda #tech #investing #ai #machinelearning',
            'label': 'SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'Not much of a hero call, but I''m doing it anyways. The bottom is in for $TWTR',
            'label': 'NON-SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'Apple expected to reveal new 10.5-inch iPad Pro at WWDC #AppleInsider $AAPL',
            'label': 'NON-SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'Steve Ballmer wants to Donate most his fortune to save the birds @Twitter $TWTR',
            'label': 'NON-SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': '$NVDA "Re: Google''s TPU" on The Motley Fool message boards:',
            'label': 'NON-SPAM',
            'created_at': datetime.utcnow()
        },
        {
            'text': 'NVIDIA''s Explosive Growth in 5 Charts @themotleyfool #stocks $NVDA',
            'label': 'NON-SPAM',
            'created_at': datetime.utcnow()
        }
    ])


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('training_data')
    op.drop_table('spam_label')
    op.drop_table('classifier')
    # ### end Alembic commands ###